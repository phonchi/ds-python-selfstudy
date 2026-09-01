#!/usr/bin/env python3
"""Playwright smoke test for curriculum visuals at a 390 px viewport.

The check serves the repository locally, exercises timeline controls, seeks both
directions, and reports control/layout overflow plus JavaScript runtime errors.
External fonts and MathJax are skipped so the test is deterministic and offline.
"""

from __future__ import annotations

import argparse
import contextlib
import http.server
import re
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from check_visuals_py import PAGES, ROOT


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        pass


@contextlib.contextmanager
def local_server():
    handler = lambda *args, **kwargs: QuietHandler(  # noqa: E731
        *args, directory=str(ROOT), **kwargs
    )
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()
            thread.join(timeout=2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--screenshots",
        type=Path,
        help="optional directory for 390 px full-page screenshots",
    )
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    with local_server() as base, sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            reduced_motion="reduce",
            locale="zh-TW",
        )

        # Keep the audit independent of CDN/network availability.
        context.route(
            "**/*",
            lambda route: route.continue_()
            if route.request.url.startswith(base)
            else route.abort(),
        )

        for name in PAGES:
            page = context.new_page()
            page.set_default_timeout(2500)
            runtime_errors: list[str] = []
            page.on("pageerror", lambda exc: runtime_errors.append(str(exc)))
            page.on(
                "console",
                lambda msg: runtime_errors.append(msg.text)
                if msg.type == "error"
                and not re.search(r"ERR_FAILED|Failed to load resource", msg.text)
                else None,
            )
            try:
                page.goto(f"{base}/{name}", wait_until="domcontentloaded")
                page.wait_for_timeout(80)

                duplicate_ids = page.evaluate(
                    """() => {
                      const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
                      return [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))];
                    }"""
                )
                if duplicate_ids:
                    failures.append(f"{name}: dynamic duplicate ids: {', '.join(duplicate_ids)}")

                overflow = page.evaluate(
                    """() => {
                      const selectors = '.viz-layout,.controls-bar,.timeline-controls,.player-controls';
                      return [...document.querySelectorAll(selectors)].flatMap((el, i) => {
                        const rect = el.getBoundingClientRect();
                        const spillsViewport = rect.left < -1 || rect.right > innerWidth + 1;
                        const spillsBox = el.scrollWidth > el.clientWidth + 2;
                        if (!spillsViewport && !spillsBox) return [];
                        const child = [...el.children].find(node => node.scrollWidth > node.clientWidth + 2);
                        return [{
                          selector: el.id ? `#${el.id}` : `${el.className || el.tagName}[${i}]`,
                          section: el.closest('section')?.id || 'top',
                          child: child ? (child.id ? `#${child.id}` : child.className || child.tagName) : '—',
                          viewport: Math.round(rect.right - innerWidth),
                          internal: el.scrollWidth - el.clientWidth,
                        }];
                      });
                    }"""
                )
                for item in overflow:
                    failures.append(
                        f"{name}: 390px overflow {item['selector']} in #{item['section']} "
                        f"via {item['child']} "
                        f"(viewport {item['viewport']}px, internal {item['internal']}px)"
                    )

                # A speed control marks a true timeline (rather than a one-shot
                # calculator).  Exercise its full contract and wait past the
                # fastest timer so a cancelled callback cannot quietly revive.
                contract_errors = page.evaluate(
                    r"""async () => {
                      const errors = [];
                      const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
                      const text = el => (el?.textContent || '').trim();
                      const speedSelector = 'select[id*="Speed" i],.runner-speed,.timeline-speed';
                      const panels = [...new Set([...document.querySelectorAll(speedSelector)]
                        .map(speed => speed.closest('.viz-panel'))
                        .filter(Boolean))];
                      for (const [index, panel] of panels.entries()) {
                        const section = panel.closest('section')?.id || 'top';
                        const speed = panel.querySelector(speedSelector);
                        const buttons = [...panel.querySelectorAll('button')];
                        const play = buttons.find(b => /播放|開始|繼續|play|▶/i.test(text(b)) && !/重設|重置|reset/i.test(text(b)));
                        const prev = buttons.find(b => /上一步|previous|prev|◂|←/i.test(text(b)));
                        const next = buttons.find(b => /下一步|單步|next|step|▸|→/i.test(text(b)) && b !== play);
                        const reset = buttons.find(b => /重設|重置|reset|↺/i.test(text(b)));
                        const counterFor = () => panel.querySelector('.runner-counter,.timeline-counter,.player-counter,[id*="Counter" i]') ||
                          [...panel.querySelectorAll('span,output')].find(el => /(?:步驟|第)?\s*\d+\s*\/\s*\d+/.test(text(el)));
                        const label = `#${section} timeline ${speed?.id || index + 1}`;
                        if (!play) errors.push(`${label}: missing Play/Pause`);
                        if (!prev) errors.push(`${label}: missing Previous`);
                        if (!next) errors.push(`${label}: missing Next/Step`);
                        if (!reset) errors.push(`${label}: missing Reset`);
                        if (!play || !reset) continue;

                        if (speed?.options?.length) {
                          const fastest = [...speed.options].reduce((best, option) =>
                            Number(option.value) < Number(best.value) ? option : best);
                          speed.value = fastest.value;
                          speed.dispatchEvent(new Event('change', {bubbles:true}));
                          speed.dispatchEvent(new Event('input', {bubbles:true}));
                        }
                        play.click();
                        await sleep(40);
                        if (!counterFor()) errors.push(`${label}: missing counter`);
                        if (!/暫停|pause|⏸/i.test(text(play)) && play.getAttribute('aria-pressed') !== 'true') {
                          errors.push(`${label}: Play control does not expose Pause state`);
                        }
                        if (next) next.click(); // Step must also cancel the timer.

                        const counter = counterFor();
                        const totalMatch = text(counter).match(/\/\s*(\d+)/);
                        const total = totalMatch ? Number(totalMatch[1]) : 0;
                        const scrubber = panel.querySelector('.runner-scrubber,.timeline-scrubber,input[id$="Seek"],input[id$="Scrubber"]');
                        if (total >= 8 && !scrubber) errors.push(`${label}: ${total} frames but no scrubber`);
                        if (scrubber && !scrubber.hidden && Number(scrubber.max) > Number(scrubber.min)) {
                          scrubber.value = scrubber.max;
                          scrubber.dispatchEvent(new Event('input', {bubbles:true}));
                          scrubber.value = scrubber.min;
                          scrubber.dispatchEvent(new Event('input', {bubbles:true}));
                        }

                        reset.click();
                        const resetCounter = text(counterFor());
                        await sleep(1050);
                        const settledCounter = text(counterFor());
                        if (resetCounter && settledCounter !== resetCounter) {
                          errors.push(`${label}: reset was revived by a pending timer (${resetCounter} -> ${settledCounter})`);
                        }
                      }
                      return errors;
                    }"""
                )
                failures.extend(f"{name}: {error}" for error in contract_errors)

                if args.screenshots:
                    page.screenshot(
                        path=str(args.screenshots / f"{Path(name).stem}-390.png"),
                        full_page=True,
                    )
            except PlaywrightError as exc:
                failures.append(f"{name}: browser check failed: {exc}")
            finally:
                for message in dict.fromkeys(runtime_errors):
                    failures.append(f"{name}: runtime error: {message}")
                page.close()

        context.close()
        browser.close()

    print(f"checked {len(PAGES)} pages at 390 px with reduced motion")
    for failure in failures:
        print("FAIL", failure)
    print(f"\n{len(failures)} browser audit error(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

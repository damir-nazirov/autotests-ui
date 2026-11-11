from playwright.sync_api import expect, sync_playwright


def test_create_complete_todos_and_remaining_count():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page()
            page.goto("https://demo.playwright.dev/todomvc/")

            todo_items = page.locator(".todo-list li")
            expect(todo_items).to_have_count(0)

            todo_input = page.get_by_role("textbox", name="What needs to be done?")
            todo_input.fill("Check payment")
            todo_input.press("Enter")
            todo_input.fill("Verify refund")
            todo_input.press("Enter")

            expect(todo_items).to_have_count(2)
            expect(page.locator(".todo-count")).to_have_text("2 items left")

            payment_item = todo_items.filter(has_text="Check payment")
            refund_item = todo_items.filter(has_text="Verify refund")
            payment_checkbox = payment_item.get_by_role(
                "checkbox", name="Toggle Todo"
            )
            refund_checkbox = refund_item.get_by_role(
                "checkbox", name="Toggle Todo"
            )

            expect(payment_item).to_have_count(1)
            expect(refund_item).to_have_count(1)
            expect(payment_checkbox).not_to_be_checked()
            expect(refund_checkbox).not_to_be_checked()

            payment_checkbox.check()

            expect(payment_checkbox).to_be_checked()
            expect(refund_checkbox).not_to_be_checked()
            expect(page.locator(".todo-count")).to_have_text("1 item left")
        finally:
            browser.close()

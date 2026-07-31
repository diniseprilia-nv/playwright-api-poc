import os
import re
import json
import urllib.request

def get_error_summary():
    log_path = "test_output.log"
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Strip ANSI escape codes
            ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
            clean_content = ansi_escape.sub("", content)
            # Find pytest short test summary
            match = re.search(r"=+\s*short test summary info\s*=+", clean_content)
            if match:
                summary = clean_content[match.start():]
                # limit to first 25 lines
                lines = summary.splitlines()[:25]
                return "\n".join(lines)
            else:
                # fallback to last 15 lines of content
                lines = clean_content.splitlines()
                return "\n".join(lines[-15:])
        except Exception as e:
            return f"Failed to parse test logs: {str(e)}"
    return "Test output log not found. The workflow may have failed during setup."

def main():
    webhook_url = os.environ.get("GOOGLE_CHAT_WEBHOOK")
    if not webhook_url:
        print("GOOGLE_CHAT_WEBHOOK environment variable not set. Skipping.")
        return

    status = os.environ.get("STATUS", "failure").lower()
    workflow_url = os.environ.get("WORKFLOW_URL", "")
    run_number = os.environ.get("RUN_NUMBER", "unknown")
    actor = os.environ.get("ACTOR", "unknown")
    branch = os.environ.get("BRANCH", "unknown")
    event_name = os.environ.get("EVENT_NAME", "unknown")
    workflow_name = os.environ.get("WORKFLOW_NAME", "API Tests")

    if status == "success":
        status_text = "SUCCESS"
        emoji = "🟢"
        image_url = "https://img.icons8.com/color/96/checked--v1.png"
    elif status == "cancelled":
        status_text = "CANCELLED"
        emoji = "⚪"
        image_url = "https://img.icons8.com/color/96/help--v1.png"
    else:
        status_text = "FAILED"
        emoji = "🔴"
        image_url = "https://img.icons8.com/color/96/cancel--v1.png"

    # Assemble Sections
    info_section = {
        "header": "<b>Run Information</b>",
        "widgets": [
            {
                "decoratedText": {
                    "startIcon": {
                        "iconUrl": "https://img.icons8.com/color/48/git.png"
                    },
                    "text": f"Branch: <b>{branch}</b>",
                    "topLabel": "Git branch"
                }
            },
            {
                "decoratedText": {
                    "startIcon": {
                        "iconUrl": "https://img.icons8.com/color/48/user-male-circle--v1.png"
                    },
                    "text": f"Triggered by: <b>{actor}</b>",
                    "topLabel": "Actor"
                }
            },
            {
                "decoratedText": {
                    "startIcon": {
                        "iconUrl": "https://img.icons8.com/color/48/activity.png"
                    },
                    "text": f"Event: <b>{event_name}</b>",
                    "topLabel": "Trigger event"
                }
            }
        ]
    }

    sections = [info_section]

    if status == "failure":
        error_msg = get_error_summary()
        # Wrap error in markdown block code for textParagraph
        error_section = {
            "header": "<b><font color=\"#FF5252\">Failure Details</font></b>",
            "widgets": [
                {
                    "textParagraph": {
                        "text": f"```\n{error_msg}\n```"
                    }
                }
            ]
        }
        sections.append(error_section)

    action_section = {
        "widgets": [
            {
                "buttonList": {
                    "buttons": [
                        {
                            "text": "View Action Run",
                            "onClick": {
                                "openLink": {
                                    "url": workflow_url
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }
    sections.append(action_section)

    card_payload = {
        "cardsV2": [
            {
                "cardId": "workflow-run-notification",
                "card": {
                    "header": {
                        "title": f"API Tests: {status_text} {emoji}",
                        "subtitle": f"{workflow_name} #{run_number}",
                        "imageUrl": image_url,
                        "imageType": "CIRCLE"
                    },
                    "sections": sections
                }
            }
        ]
    }

    # Post request to Google Chat
    data = json.dumps(card_payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json; charset=UTF-8"}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print("Status:", resp.status)
            print("Response:", resp.read().decode("utf-8"))
    except Exception as e:
        print("Failed to send Google Chat notification:", e)

if __name__ == "__main__":
    main()

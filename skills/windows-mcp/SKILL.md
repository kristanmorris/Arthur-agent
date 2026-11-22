---
name: windows-mcp
description: Control and automate the Windows operating system using the Windows-MCP server for desktop UI automation, accessibility tree inspection, mouse and keyboard simulation, app management, PowerShell, and system tasks.
---

# Windows-MCP UI & Desktop Automation

This skill equips agents with the knowledge and workflows to operate Windows 10 and 11 environments using the **Windows-MCP** protocol server. It enables visual automation, UI element discovery, input simulation, and administrative operations.

## When to Use This Skill

- Automating native Windows applications (Settings, File Explorer, Office, etc.)
- Controlling web browsers (Chrome, Edge, Firefox) via accessibility DOM extraction
- Capturing screenshots, UI element bounds, and window state
- Simulating precise mouse clicks, dragging, keyboard shortcuts, and text entry
- Executing PowerShell commands, managing processes, registry keys, and clipboard contents
- Running automated end-to-end desktop QA workflows on Windows

## Available Tools Reference

Windows-MCP exposes 21 tools grouped into four main domains:

### 1. Capture Tools
- `Screenshot`: Fast visual context capture. Supports display scaling and region cropping (`display=[i]`, `region=[l, t, r, b]`).
- `Snapshot`: Captures the UI Automation (UIA) tree with interactive element IDs and coordinates. Set `use_dom=True` for browser pages to filter out browser chrome.
- `Scrape`: Extracts text and structural content from specific elements or web areas.
- `DisplayInventory`: Lists all connected displays, resolutions, and DPI scaling factors.

### 2. Input Simulation Tools
- `Click`: Clicks by coordinate `loc=[x, y]` or by element `label=<id>` from the last Snapshot. Supports left, right, middle, and double clicks.
- `Type`: Types unicode text into active or targeted fields. Supports clearing fields before input.
- `Move`: Moves cursor to `loc=[x, y]` or element `label=<id>`. Supports drag-and-drop with `drag=True`.
- `Scroll`: Scrolls vertically or horizontally by delta ticks.
- `Shortcut`: Executes hotkeys and modifier key combos (e.g. `ctrl+c`, `alt+tab`, `win+r`).
- `MultiSelect` / `MultiEdit`: Batch operations for complex forms and list selections.

### 3. Timing & Control Status
- `Wait`: Pauses execution for a specified duration in seconds.
- `WaitFor`: Waits for text, a window, or an element to appear, avoiding polling Snapshots.
- `ControlStatus`: Checks or releases AI desktop control (`release=true`). Always release control when waiting for user actions.

### 4. System & Execution Tools
- `App`: Launches, switches foreground, or resizes applications by localized Start Menu or executable name.
- `PowerShell`: Executes PowerShell scripts and cmdlets with detached child and progress handling.
- `FileSystem`: Performs atomic filesystem operations (read, write, copy, move, delete, list, search).
- `Registry`: Queries, creates, modifies, and deletes Windows Registry values.
- `Process`: Lists active system processes and terminates target PIDs.
- `Clipboard`: Reads from and writes to the Windows clipboard with retry guards.
- `Notification`: Sends native Windows toast notifications.

## Recommended Automation Workflow

1. **Visual Context First**:
   - Begin with `Screenshot` to observe the current desktop state at low token cost.
2. **Element Identification**:
   - If exact clickable IDs are needed, run `Snapshot` (or `Snapshot(use_dom=True)` for browsers).
   - Convert coordinate offsets using scale factors returned in capture metadata.
3. **Execute Input**:
   - Prefer clicking/typing by `label=<id>` if available from Snapshot, otherwise use `loc=[x, y]`.
   - Use `Shortcut` for standard OS navigation (`win+r`, `alt+f4`, `ctrl+s`).
4. **Synchronize & Wait**:
   - Use `WaitFor` to confirm an app window or button has rendered rather than spamming screenshots.
5. **Release Control**:
   - Call `ControlStatus(release=true)` as soon as automated operations finish.

## Safety & Best Practices

- **Non-reversible Actions**: PowerShell, Registry, and FileSystem modifications cannot be undone. Always verify paths and parameters before execution.
- **User Preemption**: If the human user moves the mouse or interacts with the keyboard, yield immediately and check `ControlStatus`.
- **Browser DOM Mode**: Always set `use_dom=True` when automating web pages in Chrome, Edge, or Firefox to bypass window borders and address bars.

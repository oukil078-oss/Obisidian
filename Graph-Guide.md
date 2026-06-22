---
tags: [setup, customization, guide]
aliases: []
created: 2026-06-21
status: reference

# Graph Customization Guide 🎨

Make your Obsidian graph beautiful and well-organized! Follow these steps to customize the graph view settings.

---

## Step 1: Enable Community Plugins

In **Settings → Community Plugins**, enable (in development mode):

### Essential Plugins
- **Templater** - Use the note templates I created
- **Dataview** - Create dynamic tables and queries
- **Graph View Enhancements** - Better graph visualization

### Nice-to-Have Plugins
- **Quick Add** - Create notes with hotkeys (e.g., Ctrl/Cmd+K)
- **Excalidraw** - Hand-drawn diagrams in notes
- **Canvas** - Infinite whiteboard for connecting ideas

---

## Step 2: Configure Graph Settings

**Settings → Graph View:**

### Layout Options
```json
{
  "collapseSameTypeOfItem": false,
  "collaborationLevel": 0.85,
  "filterQuery": "",
  "linkDirection": 0,
  "showTagNodes": true,
  "showAttachedNodes": true,
  "defaultNodeColorization": "source",
  "nodeLabel": "tags",
  "nodeIcon": "",
  "showArrow": false,
  "useBarnesHutGravity": false,
  "useConcentricLayout": false
}
```

### For Pretty Graph - Recommended Settings:

1. **Node Colors:** Set to `source` (colors by tags automatically)
2. **Collaboration Level:** 0.85 (shows direct links prominently)
3. **Filter Query:** Leave empty to show everything
4. **Show Tag Nodes:** Enable for tag visualization
5. **Arrow Display:** Disable for cleaner look
6. **Use BarnessHut Gravity:** Disable for stable layout

---

## Step 3: Customize Node Colors by Tag

In **Graph View → Advanced Settings**, configure tag-based coloring:

```json
{
  "defaultColor": "#ffffff",
  "colorsByTag": {
    "#project": "#5c87ff",        // Blue for projects
    "#github": "#61afef",         // GitHub blue
    "#python": "#306998",         // Python blue
    "#javascript": "#f7df1e",      // JS yellow
    "#api": "#4ec9b0",            // Cyan for APIs
    "#webapp": "#56a6bd",         // Teal for web apps
    "#tool": "#98c379",           // Green for tools
    "#resource": "#d19a66",       # Brown for resources
    "#docs": "#e06c75",           # Red for documentation
    "#tutorial": "#e0825f",       # Orange for tutorials
    "#idea": "#bd93f9",           # Purple for ideas
    "#in-progress": "#4ec9b0",    // Active work (cyan)
    "#completed": "#98c379",      // Done items (green)
    "#planning": "#d19a66"        // Future items (brown)
  }
}
```

---

## Step 4: Configure Graph Display Modes

### View All Nodes
- Show all nodes with `Ctrl/Cmd+Shift+F`
- Filter by typing tag names in the filter box

### Collapse Less Important Nodes
- Click on generic tags to collapse them
- Keep projects and profile visible

### Zoom to Profile
- Right-click [[Profile]] → Focus on this note

---

## Step 5: Graph Style Variations

### Light Theme (Default)
Good for general overview with colorful tag nodes.

### Dark Theme
```json
{
  "theme": "dark",
  "backgroundColor": "#1a1b26",
  "nodeColor": "#ffffff",
  "tagNodeColor": "#4ec9b0"
}
```

### Monochrome (Minimalist)
```json
{
  "defaultNodeColorization": "background",
  "useMonochromeLayout": true,
  "collaborationLevel": 1.0
}
```

---

## Step 6: Dataview Integration

Add dynamic tables to notes using **Dataview** plugin:

```dataview
TABLE status as "Status"
FROM ""
WHERE tags = #project
SORT priority DESC
LIMIT 10
```

This creates a dynamic table that updates when you add/remove projects!

---

## Step 7: Canvas for Visual Organization

Use **Canvas** for drag-and-drop graph organization:

1. Create a new Canvas note
2. Drag notes from your vault onto the canvas
3. Connect them visually with lines
4. Use it as a whiteboard for project planning

---

## Step 8: Graph Optimization Tips

### For Performance
- Keep tag names short (max 20 chars)
- Avoid duplicate tags (#project-python vs #python)
- Archive old projects to reduce clutter

### For Readability  
- Use meaningful tags over generic ones
- Link related projects explicitly
- Add project descriptions in Profile table

---

## Quick Visual Reference

**What Your Graph Will Show:**

```
                    [Profile] ← Central hub (red node)
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
   [[Projects/]]               [[Library/]]
   • Blue cluster (#project)    • Multi-colored resources
   • Organized by tech stack     • Tags show categories
   
   [[Tags.md]] — Index of all tags (gray nodes)
   [[Favorites/]] — Starred items (green)
```

:::callout{type="success"}
**Pro Tip:** Every new project I clone automatically adds a node to this graph, strengthens the connections, and shows how it relates to your profile and other projects! 🌐✨
:::

---

## Maintenance Checklist

- [ ] Review graph weekly for outdated links
- [ ] Archive completed projects (move tags from #active → #completed)
- [ ] Update Profile table when adding new projects
- [ ] Keep tag list consistent (avoid creating new tags randomly)

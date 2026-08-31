# Frontend Design System

NimbusForge keeps its design system source-owned inside `frontend/`. Tailwind CSS v4 provides utilities, Radix-backed shadcn/ui patterns provide accessible primitives, and feature components compose those primitives for item workflows.

## Ownership

| Layer                         | Location                      | Responsibility                                                                            |
| ----------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------- |
| Semantic tokens               | `frontend/src/index.css`      | Shared color, type, spacing, radius, shadow, dimension, breakpoint, and transition values |
| Shared primitives             | `frontend/src/components/ui/` | Reusable, domain-neutral component contracts                                              |
| Shared application components | `frontend/src/components/`    | Cross-feature compositions such as the theme menu                                         |
| Feature components            | `frontend/src/features/`      | Domain composition and item-specific behavior                                             |
| Local utilities               | Component `className` values  | One-off layout that has no reusable semantic meaning                                      |

Do not place item concepts in `components/ui/`. Do not extract a local utility combination until it represents a repeated contract. Shared component variants use `class-variance-authority`; class composition uses `cn()` from `src/lib/utils.ts`.

## Tokens

Tokens live in `frontend/src/index.css`. Primitive values are CSS custom properties with semantic names such as `--background`, `--primary`, `--border`, `--radius-control`, and `--shadow-panel`. The `@theme inline` block exposes them to Tailwind utilities such as `bg-background`, `text-muted-foreground`, and `rounded-control`.

Light values are declared on `:root`; dark values override the same semantic names on `.dark`. Add a token only when a value represents a shared role, name it for purpose rather than appearance, define both theme values when applicable, expose it through `@theme`, and consume it through the semantic utility. Feature-specific measurements remain local.

## Components

| Component    | Purpose and variants                                                                  | States and accessibility                                                                                          |
| ------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Button       | Commands; default, secondary, outline, ghost, destructive; default, small, icon sizes | Native disabled behavior; icon-only buttons require an accessible name and tooltip/title                          |
| Input        | Single-line text entry                                                                | Pair with a visible `FormLabel`; supports native required, disabled, and invalid semantics                        |
| Select       | Choosing one value from a bounded set                                                 | Radix keyboard navigation, focus management, and accessible popup semantics                                       |
| Checkbox     | Independent binary choice                                                             | Radix checked/disabled semantics; pair with a visible label                                                       |
| Dialog       | Modal confirmation or focused task                                                    | Radix focus trap, Escape close, labelled title and description; destructive actions require explicit confirmation |
| DropdownMenu | Compact sets of row or application actions                                            | Radix arrow-key navigation, Escape close, typeahead, and focus return                                             |
| Toast        | Brief success notification                                                            | Sonner exposes a live notification region; do not use toast as the only location for errors requiring recovery    |
| Card         | A genuinely bounded tool or repeated item                                             | Header, title, description, and content composition; do not nest cards                                            |
| Table        | Scan and compare structured records                                                   | Semantic table elements; action columns need visually hidden headings and named controls                          |
| Form         | Label, description, and validation-message composition                                | Every control needs a programmatic label; validation text cannot rely on color alone                              |
| StateMessage | Loading, empty, error, and success feedback                                           | Icon and text identify state; polite live status by default and alert semantics for errors                        |

Shared props remain domain-neutral and extend native or Radix props where practical. New variants belong in the existing CVA definition rather than conditional class strings at call sites.

## Responsive And Accessible Use

Build mobile-first. The shared breakpoints are `sm` (640 px), `md` (768 px), and `lg` (1024 px). At `lg`, the item form and inventory use separate columns; below it they stack. Secondary table content may be hidden on narrow screens when the primary record identity and all actions remain available. Validate representative 320 px mobile, 768 px tablet, and 1440 px desktop viewports without horizontal overflow.

Use native elements before custom interaction. Visible focus is token-driven and must remain enabled. Dialogs and menus must retain Radix focus behavior. Dynamic loading and result states use live regions; errors include text and an icon, and loading includes text and animation. Motion is limited and should respect `prefers-reduced-motion` whenever nonessential animation is added.

## Adding Components

1. Confirm the component answers a current application need.
2. Prefer a compatible shadcn/Radix primitive and keep the generated source in `src/components/ui/`.
3. Express reusable variants with CVA and semantic tokens.
4. Put domain composition in the relevant `src/features/<feature>/` directory.
5. Document new public variants, states, keyboard behavior, and intended usage here.

The design system remains part of the frontend application. It should become a separate package only after another real consumer creates that requirement.

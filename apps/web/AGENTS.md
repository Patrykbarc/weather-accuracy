## Development

This app is a package in the pnpm workspace rooted at the repo root (`pnpm-workspace.yaml`, single `pnpm-lock.yaml`). Run `pnpm install` from the root, not from here. The store lives in the root `node_modules/.pnpm`.

Commands work from the repo root:

| Command           | Runs                                     |
| ----------------- | ---------------------------------------- |
| `pnpm web:dev`    | dev server at `localhost:4321`           |
| `pnpm web:build`  | production build to `apps/web/dist/`     |
| `pnpm web:check`  | `eslint .` + `astro check`               |
| `pnpm dev`        | web **and** the FastAPI backend together |
| `pnpm api:dev`    | backend only, at `localhost:8000`        |

Anything without a root alias goes through the filter, e.g. `pnpm --filter web codegen:openapi`. That one needs `pnpm api:dev` running, because it reads `localhost:8000/openapi.json`.

When starting the dev server yourself, use background mode:

```
pnpm --filter web exec astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`, using the same `pnpm --filter web exec` prefix from the root.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

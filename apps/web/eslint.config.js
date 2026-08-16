import js from "@eslint/js";
import { defineConfig, globalIgnores } from "eslint/config";
import eslintPluginAstro from "eslint-plugin-astro";
import eslintPluginPrettier from "eslint-plugin-prettier/recommended";
import tseslint from "typescript-eslint";

export default defineConfig([
  globalIgnores(["dist/", ".astro/", "node_modules/", "public/"]),

  js.configs.recommended,

  // Type-aware linting for .ts / .tsx
  {
    files: ["**/*.{ts,tsx}"],
    extends: [tseslint.configs.recommendedTypeChecked],
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // Same typescript-eslint rules for .astro frontmatter.
  // Must come BEFORE the astro configs — they restore astro-eslint-parser,
  // which recommendedTypeChecked would otherwise replace with the TS parser.
  {
    files: ["**/*.astro"],
    extends: [tseslint.configs.recommendedTypeChecked],
  },

  // Astro rules + a11y checks on templates
  eslintPluginAstro.configs.recommended,
  eslintPluginAstro.configs["jsx-a11y-recommended"],

  // astro-eslint-parser has no projectService support, so point it at the tsconfig
  {
    files: ["**/*.astro"],
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // Generated shadcn registry components. Recharts and Base UI hand back loose
  // types, and every `shadcn add --overwrite` would undo hand-patching.
  {
    files: ["src/components/ui/**"],
    rules: {
      "@typescript-eslint/no-unsafe-argument": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unnecessary-type-assertion": "off",
      "@typescript-eslint/restrict-template-expressions": "off",
    },
  },

  // Config files and client-side <script> blocks are outside any tsconfig project
  {
    files: ["**/*.{js,mjs,cjs}", "**/*.astro/*.ts"],
    extends: [tseslint.configs.disableTypeChecked],
  },

  // Surfaces Prettier violations as ESLint errors (the Prettier extension
  // itself reports no diagnostics). Must be LAST — it disables conflicting
  // stylistic rules from the sets above.
  eslintPluginPrettier,
]);

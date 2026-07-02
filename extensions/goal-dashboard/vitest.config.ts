import path from 'path';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tests/**/*.test.ts'],
    alias: {
      // repoContext.ts imports 'vscode' at module scope; stub it out so
      // Vitest can load the file to test its pure exports.
      vscode: path.resolve(__dirname, 'tests/mocks/vscode.ts'),
    },
  },
});

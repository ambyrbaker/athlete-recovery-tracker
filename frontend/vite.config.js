import { defineConfig } from 'vite';
// All routers support /api; WHOOP requires the prefix to be preserved.
export default defineConfig({server:{proxy:{'/api':{target:'http://127.0.0.1:8000'}}}});

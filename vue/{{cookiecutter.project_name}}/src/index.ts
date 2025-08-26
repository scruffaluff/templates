/**
 * Application entrypoint.
 */

import App from "@/App.vue";
import "@/font";
import "@/index.css";
import * as pinia from "pinia";
import * as vue from "vue";
import type { ComponentPublicInstance } from "vue";

const app = vue.createApp(App);
app.config.errorHandler = (
  err: unknown,
  instance: ComponentPublicInstance | null,
  info: string
) => {
  console.error(err);
};
app.use(pinia.createPinia()).mount("#app");

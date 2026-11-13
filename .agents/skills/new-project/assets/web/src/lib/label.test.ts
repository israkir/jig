import { expect, test } from "vitest";

import { serviceLabel } from "./label";

test("keeps the service name", () => {
  expect(serviceLabel("{{title}}")).toBe("{{title}}");
});

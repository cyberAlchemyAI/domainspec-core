import { randomUUID } from "node:crypto";

export type IdGenerator = {
  id(): string;
};

export const randomUuidGenerator: IdGenerator = {
  id: () => randomUUID(),
};

import { describe, expect, it, vi } from "vitest";

import {
  chatRequestId,
  detectAreChatBridge,
  startAreChatControlPlane,
  subscribeAreChatControlPlane,
  type AreChatEvent,
} from "./are-chat-bridge";

describe("ARE chat Tauri bridge", () => {
  it("is explicitly unavailable on the web", () => {
    expect(detectAreChatBridge(undefined)).toEqual({status: "unavailable", reason: "web-mode"});
  });

  it("connects one typed channel and binds commands to its connection", async () => {
    class MockChannel<Message> { onmessage: (message: Message) => void = () => undefined }
    const invoke = vi.fn(async (command: string, _arguments: Record<string, unknown>) => command === "chat_connect"
      ? {connectionId: 7, transport: "tauri-channel-to-are-jsonl-stdio", authorityEffect: "none"}
      : command === "chat_disconnect");
    const detection = detectAreChatBridge({__TAURI__: {core: {invoke, Channel: MockChannel}}});
    if (detection.status !== "available") throw new Error("chat bridge unavailable in fixture");
    const events: AreChatEvent[] = [];
    const connection = await detection.connect((event) => events.push(event));
    const channel = invoke.mock.calls[1]?.[1]?.onEvent as MockChannel<AreChatEvent>;
    channel.onmessage({type: "session.ready", emittedAtMs: 1, threadId: "thread-1"});
    expect(events[0]?.threadId).toBe("thread-1");

    await connection.send({type: "turn.start", requestId: "turn-1", text: "Inspect."});
    expect(invoke).toHaveBeenNthCalledWith(1, "chat_control_plane_status", {});
    expect(invoke).toHaveBeenNthCalledWith(3, "chat_replay", {connectionId: 7});
    expect(invoke).toHaveBeenNthCalledWith(4, "chat_send", {
      connectionId: 7,
      command: {type: "turn.start", requestId: "turn-1", text: "Inspect."},
    });
    await connection.disconnect();
    expect(invoke).toHaveBeenNthCalledWith(5, "chat_disconnect", {connectionId: 7});
    await connection.disconnect();
    expect(invoke).toHaveBeenCalledTimes(5);
  });

  it("produces non-empty request identities", () => {
    expect(chatRequestId("turn")).toMatch(/\S+/);
  });

  it("starts one app-owned control plane and replays events emitted before the surface subscribes", async () => {
    class MockChannel<Message> { onmessage: (message: Message) => void = () => undefined }
    const invoke = vi.fn(async (command: string, _arguments: Record<string, unknown>) => command === "chat_connect"
      ? {connectionId: 11, transport: "tauri-channel-to-are-jsonl-stdio", authorityEffect: "none"}
      : undefined);
    const candidate = {__TAURI__: {core: {invoke, Channel: MockChannel}}};

    const first = startAreChatControlPlane(candidate);
    const second = startAreChatControlPlane(candidate);
    expect(second).toBe(first);
    await first;
    const channel = invoke.mock.calls[1]?.[1]?.onEvent as MockChannel<AreChatEvent>;
    channel.onmessage({type: "session.ready", emittedAtMs: Date.now(), threadId: "thread-buffered"});

    const observed: AreChatEvent[] = [];
    const unsubscribe = subscribeAreChatControlPlane((event) => observed.push(event));
    expect(observed).toMatchObject([{type: "session.ready", threadId: "thread-buffered"}]);
    expect(invoke).toHaveBeenCalledTimes(3);
    unsubscribe();
  });
});

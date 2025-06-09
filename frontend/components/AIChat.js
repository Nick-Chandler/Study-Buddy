import {
  ChatSection,
  ChatMessages,
  ChatMessage,
  ChatInput
} from '@llamaindex/chat-ui'

export default function LLMChat({ activeMessages }) {
  return (
    <ChatSection>
      <ChatMessages>
        {activeMessages.map(msg => (
          <ChatMessage key={msg.id} role={msg.role}>
            {msg.text}
          </ChatMessage>
        ))}
      </ChatMessages>
      {/* You can hide the input if you don't want it */}
      <ChatInput hidden />
    </ChatSection>
  )
}

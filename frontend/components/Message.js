import React from "react"
import ReactMarkdown from "react-markdown"
import remarkMath from "remark-math"
import rehypeKatex from "rehype-katex"
import rehypeRaw from "rehype-raw" // Added for inline HTML rendering
import 'katex/dist/katex.min.css'
import Styles from '../styles/NewAssistant.module.css'

// Added function to style citations
function styleCitations(text) {
  // return text.replace(/【[\d:†a-zA-Z_.-]+】/g, '<span class="citation">$&</span>');
  return text.replace(/【[\d:†a-zA-Z_.-]+】/g, '');
}

export default function Message({ content }) {
  const styledContent = styleCitations(content); // Style citations before rendering

  return (
    <div className="message-card">
      <ReactMarkdown
        children={styledContent}
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex, rehypeRaw]} // Added rehypeRaw to allow HTML tags
        components={{
          code({ node, inline, className, children, ...props }) {
            return !inline ? (
              <pre className="message-code-block">
                <code {...props}>{children}</code>
              </pre>
            ) : (
              <code className="message-inline-code" {...props}>
                {children}
              </code>
            )
          },
          // Render span for citation styling
          span: ({ node, ...props }) => <span {...props} />,
          sup: ({ node, ...props }) => <sup {...props} />,
        }}
      />
    </div>
  )
}

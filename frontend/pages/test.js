import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'

const latexText = "Your 1RM is $\\text{Weight} \\times \\left(1 + \\frac{\\text{Reps}}{30}\\right)$"

export default function test() {
  return (
    <div>
      <ReactMarkdown
      children="Using the Epley formula to estimate your one-rep max (1RM) with a bench press of 95 lbs for 10 reps:

1RM = \[Weight \times (1 + \frac{Reps}{30})\]

Plugging in your numbers:

1RM = \[95 \times (1 + \frac{10}{30})\]

1RM = \[95 \times 1.333\]

1RM ≈ 127 lbs

So, your estimated one-rep max is approximately 127 lbs."
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
    />
    </div>
  )
}

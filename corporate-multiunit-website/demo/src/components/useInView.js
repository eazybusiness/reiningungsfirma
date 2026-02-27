import { useEffect, useRef, useState } from 'react'

/**
 * Custom hook that detects when an element enters the viewport.
 *
 * Args:
 *   threshold (number): Intersection threshold (0-1).
 *
 * Returns:
 *   [ref, isInView]: React ref to attach and boolean visibility state.
 */
export function useInView(threshold = 0.1) {
  const ref = useRef(null)
  const [isInView, setIsInView] = useState(false)

  useEffect(() => {
    const element = ref.current
    if (!element) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true)
          observer.unobserve(element)
        }
      },
      { threshold }
    )

    observer.observe(element)

    return () => observer.disconnect()
  }, [threshold])

  return [ref, isInView]
}

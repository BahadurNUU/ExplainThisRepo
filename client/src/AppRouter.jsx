import { Routes, Route } from "react-router"
import IntroPage from "./pages/IntroPage"
import DocPage from "./pages/DocPage"

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<IntroPage />} />
      <Route path="/doc" element={<DocPage />} />
      <Route path="*" element={<IntroPage />} />
    </Routes>
  )
}
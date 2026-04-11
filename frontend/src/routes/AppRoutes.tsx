import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Toaster } from "react-hot-toast"
import Login from "../pages/Login"
import Dashboard from "../pages/dashboard"
import RoomDetail from "../pages/RoomDetail"

function AppRoutes() {
  return (
    <BrowserRouter>
      {/* 🔥 AQUÍ VA */}
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: "#111",
            color: "#fff",
            borderRadius: "8px"
          }
        }}
      />

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/rooms/:number" element={<RoomDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
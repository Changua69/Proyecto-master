import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "../pages/Login"
import Dashboard from "../pages/dashboard"
import RoomDetail from "../pages/RoomDetail"

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/rooms" element={<RoomDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes
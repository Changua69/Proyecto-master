import { useState } from "react"
import type { CSSProperties } from "react"
import { useNavigate } from "react-router-dom"
import API from "../services/api"

type Tab = "login" | "register"

function Login() {
  const [tab, setTab] = useState<Tab>("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [role, setRole] = useState("huesped")
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const params = new URLSearchParams()
      params.append("username", email)
      params.append("password", password)
      const res = await API.post("/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      })
      localStorage.setItem("user", JSON.stringify({ ...res.data, role }))
      navigate("/dashboard")
    } catch (error: any) {
      alert(error.response ? "Credenciales incorrectas" : "Error de conexión")
    }
  }

  return (
    <div style={page}>
      <div style={card}>
        <div style={{ textAlign: "center", marginBottom: "1.5rem" }}>
          <div style={logoCircle}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </div>
          <h1 style={hotelTitle}>Marea Dorada Resort</h1>
          <p style={subtitleText}>Gestión Integral de Reservas · 24 Habitaciones</p>
        </div>

        <div style={tabWrapper}>
          <button style={{ ...tabBtn, ...(tab === "login" ? tabActive : tabInactive) }} onClick={() => setTab("login")}>
            Iniciar Sesión
          </button>
          <button style={{ ...tabBtn, ...(tab === "register" ? tabActive : tabInactive) }} onClick={() => setTab("register")}>
            Registrarse
          </button>
        </div>

        {tab === "login" && (
          <div>
            <Field label="Correo Electrónico">
              <div style={inputWrapper}>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#aaa" strokeWidth="2">
                  <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
                </svg>
                <input type="email" placeholder="usuario@ejemplo.com" style={inputInner}
                  value={email} onChange={e => setEmail(e.target.value)} />
              </div>
            </Field>
            <Field label="Contraseña">
              <div style={inputWrapper}>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#aaa" strokeWidth="2">
                  <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <input type="password" placeholder="••••••••" style={inputInner}
                  value={password} onChange={e => setPassword(e.target.value)} />
              </div>
            </Field>
            <Field label={<>Rol <span style={{ fontWeight: 400, color: "#888" }}>(Seleccionar para Demo)</span></>}>
              <select style={selectStyle} value={role} onChange={e => setRole(e.target.value)}>
                <option value="huesped">Huésped</option>
                <option value="recepcionista">Recepcionista</option>
                <option value="admin">Administrador</option>
              </select>
            </Field>
            <button style={primaryBtn} onClick={handleLogin}>Ingresar</button>
            <p style={forgotLink}>¿Olvidaste tu contraseña?</p>
          </div>
        )}

        {tab === "register" && (
          <div>
            <Field label="Nombre Completo">
              <input type="text" placeholder="Juan Pérez" style={inputBlock} />
            </Field>
            <Field label="Correo Electrónico">
              <input type="email" placeholder="usuario@ejemplo.com" style={inputBlock} />
            </Field>
            <Field label="Teléfono">
              <input type="tel" placeholder="+52 123 456 7890" style={inputBlock} />
            </Field>
            <Field label="Contraseña">
              <input type="password" placeholder="••••••••" style={inputBlock} />
            </Field>
            <Field label="Confirmar Contraseña">
              <input type="password" placeholder="••••••••" style={inputBlock} />
            </Field>
            <button style={primaryBtn}>Crear Cuenta</button>
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, children }: { label: React.ReactNode; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: "1rem" }}>
      <label style={labelStyle}>{label}</label>
      {children}
    </div>
  )
}

const page: CSSProperties = {
  minHeight: "100vh", width: "100%",
  background: "#f5f5f5",
  display: "flex", alignItems: "center", justifyContent: "center",
  padding: "2rem", boxSizing: "border-box"
}
const card: CSSProperties = {
  background: "white", borderRadius: "12px",
  border: "1px solid #eee", padding: "2rem",
  width: "100%", maxWidth: "420px"
}
const logoCircle: CSSProperties = {
  width: "56px", height: "56px", borderRadius: "50%",
  background: "#2563eb", display: "flex",
  alignItems: "center", justifyContent: "center", margin: "0 auto 1rem"
}
const hotelTitle: CSSProperties = { margin: 0, fontSize: "22px", fontWeight: 600, color: "#111" }
const subtitleText: CSSProperties = { margin: "4px 0 0", fontSize: "13px", color: "#888" }
const tabWrapper: CSSProperties = {
  display: "flex", background: "#f0f0f0",
  borderRadius: "8px", padding: "3px", marginBottom: "1.5rem"
}
const tabBtn: CSSProperties = {
  flex: 1, padding: "7px", border: "none",
  borderRadius: "6px", fontSize: "13px", cursor: "pointer"
}
const tabActive: CSSProperties = { background: "white", fontWeight: 500, color: "#111" }
const tabInactive: CSSProperties = { background: "transparent", fontWeight: 400, color: "#888" }
const labelStyle: CSSProperties = {
  fontSize: "13px", fontWeight: 500, color: "#333",
  display: "block", marginBottom: "6px"
}
const inputWrapper: CSSProperties = {
  display: "flex", alignItems: "center",
  border: "1px solid #e0e0e0", borderRadius: "8px",
  padding: "0 12px", background: "#fafafa"
}
const inputInner: CSSProperties = {
  border: "none", background: "transparent",
  padding: "10px 8px", fontSize: "14px",
  width: "100%", outline: "none", color: "#111"
}
const inputBlock: CSSProperties = {
  width: "100%", padding: "10px 12px",
  border: "1px solid #e0e0e0", borderRadius: "8px",
  background: "#fafafa", fontSize: "14px",
  color: "#111", boxSizing: "border-box" as const
}
const selectStyle: CSSProperties = {
  width: "100%", padding: "10px 12px",
  border: "1px solid #e0e0e0", borderRadius: "8px",
  background: "#fafafa", fontSize: "14px", color: "#111"
}
const primaryBtn: CSSProperties = {
  width: "100%", padding: "12px",
  background: "#111", color: "white", border: "none",
  borderRadius: "8px", fontSize: "14px", fontWeight: 500,
  cursor: "pointer", marginBottom: "1rem"
}
const forgotLink: CSSProperties = {
  textAlign: "center", fontSize: "13px",
  color: "#2563eb", cursor: "pointer", margin: 0
}

export default Login
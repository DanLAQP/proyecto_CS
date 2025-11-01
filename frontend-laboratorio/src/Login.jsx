import { useState, useEffect } from "react";

function Toast({ message, onClose }) {
  useEffect(() => {
    if (!message) return;
    const id = setTimeout(onClose, 4000);
    return () => clearTimeout(id);
  }, [message]);

  if (!message) return null;

  return (
    <div style={{ position: "fixed", top: 20, right: 20, background: "#0b6", color: "#fff", padding: "12px 16px", borderRadius: 6, boxShadow: "0 2px 8px rgba(0,0,0,0.2)" }}>
      {message}
    </div>
  );
}

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [userRole, setUserRole] = useState("");
  const [newUser, setNewUser] = useState({ username: "", password: "", rol: "tecnico" });
  const [createMsg, setCreateMsg] = useState("");
  const [toast, setToast] = useState("");

  useEffect(() => {
    // connect to SSE notifications
    const es = new EventSource("http://127.0.0.1:8000/api/accounts/notifications/stream/");
    es.onmessage = (e) => {
      try {
        const payload = JSON.parse(e.data);
        if (payload.type === "login") {
          const { username: u, login_count } = payload.data;
          setToast(`Usuario ${u} inició sesión — total: ${login_count}`);
        }
      } catch (err) {
        console.error("failed parse sse", err);
      }
    };
    es.onerror = (err) => {
      console.warn("SSE error", err);
      // EventSource auto-reconnects; we don't close here
    };
    return () => es.close();
  }, []);

  // LOGIN
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/api/accounts/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include",
      });

      if (!res.ok) throw new Error("Usuario o contraseña incorrecta");

      const data = await res.json();
      setMessage("Login exitoso!");
      setUserRole(data.rol || "user");
      // show singleton state returned by the backend
      if (data.app_singleton) {
        setToast(`Logins totales: ${data.app_singleton.login_count}`);
      }
      console.log(data);
    } catch (err) {
      setMessage(err.message);
    }
  };

  // CREAR NUEVO USUARIO (solo admin)
  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/api/accounts/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser),
        credentials: "include",
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Error al crear usuario");
      setCreateMsg(`Usuario ${newUser.username} creado!`);
    } catch (err) {
      setCreateMsg(err.message);
    }
  };

  return (
    <div style={{ display: "flex", minHeight: "80vh", alignItems: "center", justifyContent: "center", background: "#f5f7fb" }}>
      <div style={{ width: 360, padding: 24, borderRadius: 8, background: "#fff", boxShadow: "0 6px 18px rgba(0,0,0,0.08)" }}>
        <h2 style={{ marginTop: 0, marginBottom: 8, textAlign: "center" }}>Iniciar sesión</h2>
        <p style={{ color: "#666", textAlign: "center", marginTop: 0 }}>Accede a tu cuenta</p>

        <form onSubmit={handleLogin} style={{ display: "grid", gap: 10 }}>
          <input style={{ padding: "10px 12px", borderRadius: 6, border: "1px solid #ddd" }}
            type="text" placeholder="Usuario" value={username} onChange={(e) => setUsername(e.target.value)} />

          <input style={{ padding: "10px 12px", borderRadius: 6, border: "1px solid #ddd" }}
            type="password" placeholder="Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} />

          <button type="submit" style={{ padding: "10px 12px", borderRadius: 6, border: "none", background: "#2563EB", color: "white", cursor: "pointer" }}>Entrar</button>
        </form>

        {message && <p style={{ marginTop: 12, color: message.includes('exitos') ? 'green' : 'red' }}>{message}</p>}

        {/* SOLO ADMIN */}
        {userRole === "admin" && (
          <div style={{ marginTop: 18 }}>
            <h3>Crear Usuario</h3>
            <form onSubmit={handleCreateUser} style={{ display: "grid", gap: 8 }}>
              <input type="text" placeholder="Nuevo usuario" value={newUser.username} onChange={(e) => setNewUser({ ...newUser, username: e.target.value })} />
              <input type="password" placeholder="Contraseña" value={newUser.password} onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} />
              <select value={newUser.rol} onChange={(e) => setNewUser({ ...newUser, rol: e.target.value })}>
                <option value="tecnico">Técnico</option>
                <option value="admin">Admin</option>
              </select>
              <button type="submit" style={{ padding: 8, borderRadius: 6, background: '#10B981', color: 'white', border: 'none' }}>Crear Usuario</button>
            </form>
            {createMsg && <p style={{ marginTop: 8 }}>{createMsg}</p>}
          </div>
        )}

      </div>
      <Toast message={toast} onClose={() => setToast("")} />
    </div>
  );
}

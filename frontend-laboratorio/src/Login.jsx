import { useState } from "react";

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [userRole, setUserRole] = useState(""); // guarda el rol
  const [newUser, setNewUser] = useState({ username: "", password: "", rol: "tecnico" });
  const [createMsg, setCreateMsg] = useState("");

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
      setUserRole(data.rol || "user"); // suponiendo que el backend devuelve el rol
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
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      <p>{message}</p>

      {/* SOLO ADMIN */}
      {userRole === "admin" && (
        <div>
          <h2>Crear Usuario</h2>
          <form onSubmit={handleCreateUser}>
            <input
              type="text"
              placeholder="Nuevo usuario"
              value={newUser.username}
              onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
            />
            <input
              type="password"
              placeholder="Contraseña"
              value={newUser.password}
              onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
            />
            <select
              value={newUser.rol}
              onChange={(e) => setNewUser({ ...newUser, rol: e.target.value })}
            >
              <option value="tecnico">Técnico</option>
              <option value="admin">Admin</option>
            </select>
            <button type="submit">Crear Usuario</button>
          </form>
          <p>{createMsg}</p>
        </div>
      )}
    </div>
  );
}

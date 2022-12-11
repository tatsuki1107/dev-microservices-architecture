import react, { useState } from "react";
import './App.css';
import { useAuth } from "./AuthProvider";

const defaultState = { "username": "", "password": "" }

const Login = () => {
  const [state, setState] = useState(defaultState);
  const { onLogin } = useAuth()

  return (
    <>
      <div className="App">
        <h1>ログインする</h1>
        <input
          placeholder="johndoeを入力"
          onChange={(e) => setState(prev => ({ ...prev, "username": e.target.value }))} />
        <input
          placeholder="secretを入力"
          onChange={(e) => setState(prev => ({ ...prev, "password": e.target.value }))}
        />
        <button onClick={() => onLogin(state)}>送信</button>
      </div>
    </>
  );
}

export default Login;

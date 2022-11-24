import react, { useState, useEffect } from "react";
import axios from "axios";
import './App.css';

const config = {
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  }
}

const defaultState = { "username": "", "password": "" }
const RESTURL = "http://localhost:5000";

const App = () => {
  const [state, setState] = useState(defaultState);
  const [token, setToken] = useState("");
  const users_me_config = {

    Authorization: `Bearer ${sessionStorage.getItem('token')}`

  }
  const onFinish = async () => {
    try {
      await axios.post(`${RESTURL}/token`, state, config)
        .then(res => {
          setToken(res?.data.access_token)
          sessionStorage.setItem("token", res?.data.access_token)
        })
    } catch (e) {
      console.error(e)
    }
  }
  useEffect(() => {
    (async () => {
      try {
        console.log(users_me_config)
        await axios.post(`${RESTURL}/users/me/`, users_me_config)
          .then(res => console.log(res?.data))
      } catch (e) {
        console.error(e)
      }

    })()
    setToken(sessionStorage.getItem("token"))
  }, [])
  return (
    <div className="App">
      {!token ?
        <div>
          <h1>ログインする</h1>
          <input
            placeholder="name"
            onChange={(e) => setState(prev => ({ ...prev, "username": e.target.value }))} />
          <input
            placeholder="password"
            onChange={(e) => setState(prev => ({ ...prev, "password": e.target.value }))}
          />
          <button onClick={onFinish}>送信</button>
        </div> :
        <div>
          <p>アクセストークン: {token}</p>
          <a href="http://localhost:3001">マイクロサービス化したサイトに飛ぶ</a>
        </div>
      }

    </div>
  );
}

export default App;

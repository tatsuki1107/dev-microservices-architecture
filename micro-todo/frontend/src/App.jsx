import react, { useState, useEffect } from "react";
import axios from "axios";
import './App.css';

const AUTHURL = "http://localhost:5000";
const RESTURL = "http://localhost:5001";

const App = () => {
  axios.defaults.withCredentials = true;
  const [user, setUser] = useState({})
  const [todos, setTodos] = useState([])
  useEffect(() => {
    (async () => {
      try {
        await axios.get(`${AUTHURL}/todo_auth`).then(res => {
          setUser(res?.data)
          axios.post(`${RESTURL}/user`, res?.data).then(res => {
            setTodos(res?.data)
          })
        })
      } catch (e) {
        console.error(e)
        if (e.response.status === 401) {
          alert("セッション切れです、ログインし直して下さい。")
          window.location.href = "http://localhost:3000/login";
        }
      }
    })()
  }, [])
  return (
    <div className="App">
      <h1>マイクロtodoアプリ</h1>
      <p>ようこそ　{user.username}さん</p>
      <div>
        {todos.map((item, i) => {
          return (
            <div key={i}>
              <h2>todo: {item.todo}</h2>
              <p>日付: {item.date}</p>
            </div>
          )
        })}
      </div>
    </div>
  );
}

export default App;

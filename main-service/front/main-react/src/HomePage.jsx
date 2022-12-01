import React, { useState, useEffect } from "react";
import { useAuth } from "./AuthProvider";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { AUTHURL, config } from "./AuthProvider";

const HomePage = () => {
  axios.defaults.withCredentials = true;
  const TODOURL = "http://localhost:5001"
  const { user } = useAuth();
  const [todo, setTodo] = useState({})
  const navigate = useNavigate();
  //const config = {
  // headers: { "Content-Type": "application/json" }
  //}

  const getTodo = async () => {
    try {
      const data = { "micro_id": user.micro_id }
      await axios.post(`${TODOURL}/user_todo`, data).then(res => setTodo(res?.data))
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div style={{ "textAlign": "center" }}>
      <h1>Home Page</h1>
      <h2>your profile</h2>
      <p>name: {user.username}</p>
      <p>email: {user.email}</p>

      <a href="http://localhost:3001">マイクロ化したtodoアプリへ遷移</a>
      <button onClick={getTodo}>はじめにやるべきtodoを表示</button>

      <h2>手を付けるべきこと: {todo.todo}</h2>
      <h3>期日: {todo.date}</h3>
    </div>
  );
};

export default HomePage;

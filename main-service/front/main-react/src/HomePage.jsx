import React, { useState, useEffect } from "react";
import { useAuth } from "./AuthProvider";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { AUTHURL } from "./AuthProvider";

const HomePage = () => {
  const { user } = useAuth();
  const [todo, setTodo] = useState()
  const navigate = useNavigate();
  const config = {
    headers: { "Content-Type": "application/json" }
  }

  const getTodo = async () => {
    try {
      const data = { "micro_id": user.micro_id }
      await axios.post(`${AUTHURL}/todos`, data, config).then(res => console.log(res?.data))
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

      <p>{todo}</p>
    </div>
  );
};

export default HomePage;

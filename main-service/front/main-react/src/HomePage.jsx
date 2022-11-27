import React, { useState, useEffect } from "react";
import { useAuth } from "./AuthProvider";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { RESTURL } from "./AuthProvider";

const HomePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div style={{ "textAlign": "center" }}>
      <h1>Home Page</h1>
      <h2>your profile</h2>
      <p>name: {user.username}</p>
      <p>email: {user.email}</p>

      <a href="http://localhost:3001">マイクロ化したtodoアプリへ遷移</a>
      <h2>はじめにやるべきtodo</h2>
      <p>ここでapi連携</p>
    </div>
  );
};

export default HomePage;

import React, { useState, createContext, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const AuthContext = createContext();
export const AUTHURL = "http://localhost:5000";
const config = {
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  }
}

const AuthProvider = ({ children }) => {
  axios.defaults.withCredentials = true;
  const [user, setUser] = useState({})
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate();

  const onLogin = async (state) => {
    try {
      await axios.post(`${AUTHURL}/token`, state, config).then(res => {
        console.log(res?.data)
      });
      navigate('/')
    } catch (e) {
      console.error(e)
      if (e.response.status === 401) {
        alert(' name またはパスワードが違います。')
      }
    }
  }
  console.log(user)

  useEffect(() => {
    (async () => {
      try {
        await axios.get(`${AUTHURL}/users/me`).then(res => {
          setUser(res?.data)
        })
      } catch (e) {
        console.error(e)
        if (e.response.status === 401) {
          alert('セッション切れです、ログインし直して下さい。');
          navigate('/login');
        }
      }
    })()
    setLoading(false);
  }, [])
  if (!loading) {
    return <AuthContext.Provider value={{ user, onLogin }}>{children}</AuthContext.Provider>;
  }
};

export default AuthProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};

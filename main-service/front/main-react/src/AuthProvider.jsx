import React, { useState, createContext, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const AuthContext = createContext();
export const RESTURL = "http://localhost:5000";
const config = {
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  }
}

const AuthProvider = ({ children }) => {
  const [token, setToken] = useState("")
  const [user, setUser] = useState({})
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate();

  const onLogin = async (state) => {
    try {
      await axios.post(`${RESTURL}/token`, state, config).then(res =>
        setToken(res?.data.access_token));
    } catch (e) {
      console.error(e)
    } finally {
      navigate('/');
    }
  }

  useEffect(() => {
    (async () => {
      try {
        await axios.get(`${RESTURL}/users/me`).then(res => setUser(res?.data))
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    })()
  }, [token])
  if (!loading) {
    return <AuthContext.Provider value={{ user, onLogin }}>{children}</AuthContext.Provider>;
  }
};

export default AuthProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};

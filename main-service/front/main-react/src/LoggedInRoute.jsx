import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const LoggedInRoute = ({ children }) => {
  const { token } = useAuth();

  if (!token) {
    return <Navigate to="/login" />
  }
  return children;
};

export default LoggedInRoute;

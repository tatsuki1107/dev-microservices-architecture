import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login";
import HomePage from "./HomePage";
import AuthProvider from "./AuthProvider";
import LoggedInRoute from "./LoggedInRoute";

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/"
            element={
              <LoggedInRoute>
                <HomePage />
              </LoggedInRoute>
            } />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;

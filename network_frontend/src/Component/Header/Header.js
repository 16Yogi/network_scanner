import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './header.css';

export default function Header() {
  const navigate = useNavigate();
  const [userFullname, setUserFullname] = useState(null);

  useEffect(() => {
    const fullname = localStorage.getItem("userFullname");
    if (fullname) {
      setUserFullname(fullname);
    }
  }, []);

  const handleLogout = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/logout/", {
      method: "POST",
      credentials: "include",
    });

    const data = await res.json();
    alert(data.message || "Logged out");

    // Clear localStorage and redirect
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userFullname");
    setUserFullname(null);
    navigate("/login");
  };

  return (
    <div className='container-fluid header'>
      <div className='container'>
        <nav className="navbar navbar-expand-lg navbar-light">
          <Link className="navbar-brand text-bold text-info" to="/">Network Scanner</Link>

          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item active">
                <Link className="nav-link" to="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/scan">Scan</Link>
              </li>
            </ul>

            <div className="form-inline my-2 my-lg-0">
              {userFullname ? (
                <>
                  <span className="navbar-text mr-3">Welcome, {userFullname}</span>
                  <button className="btn btn-outline-danger my-2 my-sm-0" type="button" onClick={handleLogout}>Logout</button>
                </>
              ) : (
                <>
                  <Link className='nav-link' to="/login">
                    <button className="btn btn-outline-primary my-2 my-sm-0" type="button">Login</button>
                  </Link>
                  <Link className='nav-link' to="/registration">
                    <button className="btn btn-outline-success my-2 my-sm-0" type="button">Registration</button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </nav>
      </div>
    </div>
  );
}

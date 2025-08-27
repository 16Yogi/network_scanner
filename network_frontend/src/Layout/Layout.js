import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../Component/Header/Header';
import Footer from '../Component/Footer/Footer';

export default function Layout() {
  return (
    <>
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

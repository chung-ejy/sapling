import React , { useContext, Fragment }from 'react';
import { Link } from 'react-router-dom';
import Icon from '../../assets/favicon-16x16.png'
import DataContext from '../../context/data/dataContext'
const Header = () => {

    const dataContext = useContext(DataContext)
    const { isAuth, logout } = dataContext
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link to="/" className="navbar-brand">
                    <img alt="" src={Icon} />
                    {" mistletoe"}
                </Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <Link to="/" className="nav-link">
                                Home
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/learn" className="nav-link">
                                Learn
                            </Link>
                        </li>
                        {isAuth === true ? 
                            <Fragment><li className="nav-item"><Link to="/dashboard" className="nav-link">
                                Dashboard
                            </Link></li>
                            <li className='nav-item' onClick={() => logout()}><div className="nav-link">Logout</div></li>
                        </Fragment>:
                        <li className="nav-item">
                            <Link to="/login" className="nav-link">
                                Login
                            </Link>
                        </li>}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Header;

import 'index.scss';

import * as serviceWorker from 'serviceWorker';

import App from 'components/App';
import { Provider } from 'react-redux';
import React from 'react';
import ReactDOM from 'react-dom';
import store from 'state/store';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ClassPage from 'components/classpage/ClassPage';
import Titlebar from 'components/titlebar/Titlebar';

ReactDOM.render(
  <React.StrictMode>
    <Provider store={ store }>
      <Titlebar />
      <div className={"mainContainer"}>
        <Router>
          <Routes>
            <Route exact path="/" Component={App} />
            <Route path="/class/:classId" Component={ClassPage} />
          </Routes>
        </Router>
      </div>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

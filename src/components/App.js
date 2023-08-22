import React, { Fragment, useEffect, useState } from 'react';
import Titlebar from 'components/titlebar/Titlebar';
import ClassRow from 'components/classrow/Classrow';
import axios from 'axios';
import { get } from 'utils/requests';


function App() {
  const [classNameInput, setClassNameInput] = useState("");
  const [classes, setClasses] = useState([]);
  
  useEffect(() => {
    axios.get('http://localhost:3001/api/get_classes')
    .then((response) => {
      console.log(response);
      if (response.data["status"] === "success") {
        setClasses(response.data["classes"]);
      }
    }).catch((error) => {
      console.log(error);
    });
  }, []);

  function addClass() {
    axios.post('http://localhost:3001/api/add_class', {
      name: classNameInput
    }).then((response) => {
      console.log(response);
      if (response.data["status"] === "success") {
        // TODO: Add class to list
      }
    }).catch((error) => {
      console.log(error);
    });
  }
  return (
    <Fragment>
      {classes.map((classObj) => (
      <ClassRow key={classObj.id} name={classObj.name} id={classObj.id} />
      ))}

      <input type="text" value={classNameInput} onChange={(e) => setClassNameInput(e.target.value)} />
      <button onClick={addClass}>Add Class</button>
    </Fragment>
  );
}

export default App;

import { Grid } from '@mui/material';
import React, { Fragment, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

function LinkRow({title, link}) {
    return (
        <Grid container style={{border: "1px blue solid", height: "30px"}}>
            <Grid item xs={4} style={{border: "1px red solid"}}>
                {title}
            </Grid>
            <Grid item xs={8}>
                {link}
            </Grid>
        </Grid>
    );
}

function ClassPage() {
    const navigate = useNavigate();
    const [linkRows, setLinkRows] = useState([]);
    const { classId } = useParams();

    useEffect(() => {
        axios.get('http://localhost:3001/api/get_class_info', {
            params: {
                classId: classId
            }
        }).then((response) => {
            console.log(response);
            if (response.data["status"] === "success") {
                setLinkRows(response.data["links"]);
            }
        }).catch((error) => {
            console.log(error);
        });
    }, []);

    function navigateHome() {
        navigate('/');
    }

    function addLinkRow() {
        setLinkRows([...linkRows, <LinkRow key={linkRows.length} title={"title"} link={"link"} />]);
    }

    return (
        <Fragment>
            <button onClick={navigateHome}>Back</button>
            Class Page
            <Grid container>
                {linkRows}
                <Grid item xs={12} style={{border: "1px blue solid", height: "30px"}} onClick={addLinkRow}>
                    <button>Add Row</button>
                </Grid>
            </Grid>
        </Fragment>
    );
}

export default ClassPage;
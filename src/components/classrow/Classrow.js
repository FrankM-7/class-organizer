import React, { useEffect } from 'react';
import { Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Classrow({id, name}) {
    const navigate = useNavigate();
    function navigateClass() {
        navigate("/class/" + id);
    }
    return (
        <div style={{height: "80px", padding: "5px"}} onClick={navigateClass}>
            <Paper elevation={3} style={{height: "100%", width: "100%"}}>
                {name}
            </Paper>
        </div>
    );
}

export default Classrow;
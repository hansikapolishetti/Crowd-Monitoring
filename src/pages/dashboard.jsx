import React from "react";

function Dashboard(){

return(

<div className="bg-gray-900 h-screen text-white p-6">

<h1 className="text-3xl mb-6">
Crowd Monitoring Dashboard
</h1>

<div className="bg-gray-800 p-4 rounded">

<p>Camera Feed</p>

<img src="http://127.0.0.1:5000/video" width="700"/>

</div>

</div>

)

}

export default Dashboard
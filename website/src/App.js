import "./App.css";
import data from "./predicted_data.json";

function App() {
  //  const data_json = {data}
  //  console.log(data_json);
  //  data_json.forEach(element => {
  //   console.log(element);
  //  });

  return (
    <div className="App">
      <div className="container mt-5">
        <h1 className='text-center'>Cyber Bullying Report 2023</h1>
      
      
        <div className="col-md-12 ">
          <table className="table table-bordered">
            <thead className="thead-dark">
              <tr>
                <th scope="col-md-6">Name</th>
                <th scope="col-md-6">Comments</th>
                <th scope="col-md-6">Satus</th>
              </tr>
            </thead>
            <tbody>
            
      
              {data.names.map((name,index)=>(
                <tr>
                  <td className="text_align">{name}</td>
                  <td className="text_align">{data['comments'][index]}</td>
                  <td>
                     <p
                       className={
                         data['classname'][index] === "Non-Bullying"
                           ? "text-success "
                           : "text-danger "
                       }
                     >
                       {data['classname'][index]}
                     </p>
                   </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        </div>
     
    </div>
  );
}

export default App;

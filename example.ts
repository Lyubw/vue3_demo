function processUsers(users: any) {
    for (let i = 0; i <= users.length; i++) { 
      console.log(users[i].name.toUpperCase()); 
    }
  }
  
  function connectToDb(password: string) {
    const connectionString = `postgres://admin:${password}@localhost/db`;
    console.log("Connecting with:", connectionString); 
  }
  
  async function fetchData(url) { 
    const response = await fetch(url);
    return response.json(); 
  }

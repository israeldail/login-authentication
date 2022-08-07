const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      token: null,
      message: null,
      demo: [
        {
          title: "FIRST",
          background: "white",
          initial: "white",
        },
        {
          title: "SECOND",
          background: "white",
          initial: "white",
        },
      ],
    },
    actions: {
      // Use getActions to call a function within a fuction

      syncTokenFromSessionStorage: () => {
        const token = sessionStorage.getItem("token");
        console.log(
          "application just loaded, syncing the session storage token"
        );
        if (token && token != "" && token != undefined)
          setStore({ token: token });
      },

	  signup: async (email,password) => {
		const opts = {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				email: email,
				password: password,
			})
		}

		try {
			const resp = await fetch("https://3001-israeldail-loginauthent-5k621p74mfo.ws-us59.gitpod.io/api/signup",
            opts)
			if(resp.status !== 200) {
				alert('there was an error signing up')
				return false;
			}
			const data = await resp.json();
			console.log("this came from the backend", data)
			
		} catch(error) {
			console.error('there has been an error with the sign up')
		}
	  },

      login: async (email, password) => {
        const opts = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        };

        try {
          const resp = await fetch(
            "https://3001-israeldail-loginauthent-5k621p74mfo.ws-us59.gitpod.io/api/token",
            opts
          );
          if (resp.status !== 200) {
            alert("there has been some error");
            return false;
          }

          const data = await resp.json();
          console.log("this came from the backend", data);
          sessionStorage.setItem("token", data.access_token);
          setStore({ token: data.access_token });
          return true;
        } catch (error) {
          console.error("There has been an error logging in");
        }
      },

      logout: () => {
        sessionStorage.removeItem("token");
        console.log("Logging out");
        setStore({ token: null });
      },

      getMessage: async () => {
        const store = getStore();
        const opts = {
          headers: {
            Authorization: "Bearer " + store.token,
          },
        };
        //fetch request from backend
        try {
          const resp = await fetch(process.env.BACKEND_URL + "/api/hello");
          const data = await resp.json();
          setStore({ message: data.message });
          // don't forget to return something, that is how the async resolves
          return data;
        } catch (error) {
          console.log("Error loading message from backend", error);
        }
      },
    },
  };
};

export default getState;

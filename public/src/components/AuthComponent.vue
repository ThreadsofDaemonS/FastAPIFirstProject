<template>
  <div>
    <h2>Registration</h2>
    <form @submit.prevent="register">
      <div>
        <label for="registerName">Name:</label>
        <input type="text" id="registerName" v-model="registerName" />
      </div>
      <div>
        <label for="registerAge">Age:</label>
        <input type="text" id="registerAge" v-model="registerAge" />
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <h2>Authorization</h2>
    <form @submit.prevent="login">
      <div>
        <label for="loginName">Name:</label>
        <input type="text" id="loginName" v-model="loginName" />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuthComponent",

  data() {
    return {
      registerName: "",
      registerAge: "",
      loginName: "",
    };
  },
  methods: {
    async register() {
      const response = await axios.post("http://127.0.0.1:8000/users", {
        name: this.registerName,
        age: Number(this.registerAge),
      });
      console.log("Register success: " + response.data);
    },
    async login() {
      const response = await axios.get(
        `http://127.0.0.1:8000/users/${this.loginName}`
      );
      if (response.data) {
        this.$emit("handleAuth");
      } else {
        alert("User not found");
      }
    },
  },
};
</script>

<style></style>

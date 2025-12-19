<template>
  <div class="login-container">
    <h2>Login</h2>
    <Form :model="form" @submit.prevent="handleLogin">
      <FormItem label="Username">
        <Input v-model="form.name" placeholder="Enter username" />
      </FormItem>
      <FormItem label="Password">
        <Input type="password" v-model="form.password" placeholder="Enter password" />
      </FormItem>
      <FormItem>
        <Button type="primary" @click="handleLogin">Login</Button>
      </FormItem>
    </Form>
  </div>
</template>

<script>
import { loginUser } from "@/api/auth-api";

export default {
  name: "Login",
  data() {
    return {
      form: {
        name: "",
        password: "",
      },
    };
  },
  methods: {
    async handleLogin() {
      try {
        const result = await loginUser(this.form);
        if (result.error) {
          this.$Message.error(result.error);
        } else {
          this.$Message.success(`Welcome ${result.name}`);
          // Save login info to localStorage (or Vuex)
          localStorage.setItem("user", JSON.stringify(result));
          // Redirect to users page
          this.$router.push({ name: "users" });
        }
      } catch (err) {
        this.$Message.error("Login failed");
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 100px auto;
}
</style>

<template>
  <div class="profile">
    <!--    <img alt="Vue logo" src="../assets/logo.png">-->
    <UserProfile/>
  </div>
</template>

<script>
import UserProfile from "../components/UserProfile";
export default {
  name: "Profile",
  components: {
    UserProfile
  }
}
</script>

<style scoped>

</style>
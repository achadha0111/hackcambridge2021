<template>
  <div>
    <div class = "md-layout">
      <div class="md-layout-item"></div>
      <div class="md-layout-item md-layout md-gutter">

        <md-card class="personal-info">
          <md-card-header>
            <md-avatar class="md-avatar-icon md-medium md-primary">A</md-avatar>
            <div class="md-title">Name</div>
            <div class="md-subhead">Aayush Chadha</div>
          </md-card-header>
        </md-card>

        <div class="md-layout-item key-stats">
          <md-card class="md-accent">
            <md-card-header>
              <div class="md-title">30%</div>
              <div class="md-subhead">Misinformation protection level</div>
            </md-card-header>
          </md-card>
        </div>

        <div class="md-layout-item key-stats">
          <md-card class="md-accent">
            <md-card-header>
              <div class="md-title">Low</div>
              <div class="md-subhead">Political Engagement</div>
            </md-card-header>
          </md-card>
        </div>

        <md-card>
          <md-card-header>
            <div class="md-title">Achievements</div>
            <div class="md-subhead">This is a list of achievements you have unlocked.</div>
          </md-card-header>
          <md-card-content>
            <md-list>
              <md-list-item>
                <md-icon class="md-size-2x">flutter_dash</md-icon>
                Bird Eye: <span>You identified more than 80% fake videos and headlines.</span>
              </md-list-item>

              <md-list-item>
                <md-icon class="md-size-2x">connect_without_contact</md-icon>
                Engaged: <span>Engaged with content from across the political spectrum.</span>
              </md-list-item>

              <md-list-item>
                <md-icon class="md-size-2x">mood</md-icon>
                Opinionated: <span>You expressed an opinion on a political issue.</span>
              </md-list-item>

            </md-list>
          </md-card-content>
        </md-card>

      </div>
      <div class="md-layout-item"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserProfile"
}
</script>

<style lang="scss" scoped>


span{
  color: grey;
}
.personal-info {
  width: 100%;
  margin-bottom: 5%;
}

.key-stats {
  margin-bottom: 5%;
}
</style>
export const socketActions = {
  SOCKET_release_version(data) {
    this.releaseVersion = data.releaseVersion
  },
  SOCKET_load_end() {
    this.dataLoaded = true
  },
}

export interface User {
  id: string;
  /** Full display name including suffix if any ("Christy Harris, EdD"). */
  fullName: string;
  /** First name for greetings. */
  firstName: string;
  /** 2-letter monogram for the avatar. */
  initials: string;
}

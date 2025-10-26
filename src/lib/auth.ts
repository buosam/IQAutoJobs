import { User } from './types';

export const storeUserSession = (user: User) => {
  const userToStore = { first_name: user.first_name, role: user.role };
  localStorage.setItem("user", JSON.stringify(userToStore));
};

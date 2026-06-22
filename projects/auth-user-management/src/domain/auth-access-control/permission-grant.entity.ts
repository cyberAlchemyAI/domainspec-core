export type GrantEffect = "ALLOW" | "DENY";

export type PermissionGrant = {
  grantId: string;
  granteeType: "role" | "principal";
  granteeKey: string;
  permissionKey: string;
  effect: GrantEffect;
  createdAt: Date;
};

export type UpsertPermissionGrantInput = {
  granteeType: "role" | "principal";
  granteeKey: string;
  permissionKey: string;
  effect: GrantEffect;
};

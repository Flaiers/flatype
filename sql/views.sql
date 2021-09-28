ALTER TABLE auth_group RENAME TO groups;
ALTER TABLE auth_group_permissions RENAME TO group_permissions;
ALTER TABLE auth_permission RENAME TO permissions;

CREATE VIEW auth_group AS
    SELECT *
    FROM groups;

CREATE VIEW auth_group_permissions AS
    SELECT *
    FROM group_permissions;

CREATE VIEW auth_permission AS
    SELECT *
    FROM permissions;
